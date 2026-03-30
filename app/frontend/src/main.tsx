import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import { PrototypeProvider } from "./providers/PrototypeProvider";
import { ThemeProvider, applyTheme, getPreferredTheme } from "./providers/ThemeProvider";
import "./styles.css";

applyTheme(getPreferredTheme());

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ThemeProvider>
      <PrototypeProvider>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </PrototypeProvider>
    </ThemeProvider>
  </React.StrictMode>
);
