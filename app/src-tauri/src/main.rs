#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::Command;
use tauri::Manager;

fn start_python_server() {
    let is_dev = cfg!(debug_assertions);

    if is_dev {
        #[cfg(target_os = "windows")]
        let _ = Command::new("python")
            .args(&["src/server.py"])
            .spawn();

        #[cfg(not(target_os = "windows"))]
        let _ = Command::new("python3")
            .args(&["src/server.py"])
            .spawn();
    } else {
        let exe_name = if cfg!(target_os = "windows") {
            "triur-brain.exe"
        } else {
            "triur-brain"
        };
        let _ = Command::new(exe_name).spawn();
    }
}

#[tauri::command]
fn minimize_window(window: tauri::Window) {
    let _ = window.minimize();
}

#[tauri::command]
fn maximize_window(window: tauri::Window) {
    if window.is_maximized().unwrap_or(false) {
        let _ = window.unmaximize();
    } else {
        let _ = window.maximize();
    }
}

#[tauri::command]
fn close_window(window: tauri::Window) {
    let _ = window.close();
}

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            start_python_server();
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            minimize_window,
            maximize_window,
            close_window,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
