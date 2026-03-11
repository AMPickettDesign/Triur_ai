#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::{Command, Child};
use std::sync::Mutex;
use tauri::{Manager, State};

struct PythonServer(Mutex<Option<Child>>);

fn start_python_server() -> Option<Child> {
    // Try bundled executable first (production)
    // Fall back to python script (development)
    let is_dev = cfg!(debug_assertions);

    if is_dev {
        // Development — run Python directly
        #[cfg(target_os = "windows")]
        let cmd = Command::new("python")
            .args(&["-m", "flask", "--app", "src/server.py", "run", "--host=127.0.0.1", "--port=5000"])
            .spawn();

        #[cfg(not(target_os = "windows"))]
        let cmd = Command::new("python3")
            .args(&["-m", "flask", "--app", "src/server.py", "run", "--host=127.0.0.1", "--port=5000"])
            .spawn();

        cmd.ok()
    } else {
        // Production — use bundled executable
        let exe_name = if cfg!(target_os = "windows") {
            "triur-brain.exe"
        } else {
            "triur-brain"
        };

        Command::new(exe_name)
            .spawn()
            .ok()
    }
}

#[tauri::command]
fn minimize_window(window: tauri::Window) {
    window.minimize().unwrap();
}

#[tauri::command]
fn maximize_window(window: tauri::Window) {
    if window.is_maximized().unwrap_or(false) {
        window.unmaximize().unwrap();
    } else {
        window.maximize().unwrap();
    }
}

#[tauri::command]
fn close_window(window: tauri::Window) {
    window.close().unwrap();
}

fn main() {
    tauri::Builder::default()
        .manage(PythonServer(Mutex::new(None)))
        .setup(|app| {
            let server_state: State<PythonServer> = app.state();
            let child = start_python_server();
            *server_state.0.lock().unwrap() = child;
            Ok(())
        })
        .on_window_event(|event| {
            if let tauri::WindowEvent::CloseRequested { .. } = event.event() {
                // Python server cleanup happens via OS process tree
            }
        })
        .invoke_handler(tauri::generate_handler![
            minimize_window,
            maximize_window,
            close_window,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
