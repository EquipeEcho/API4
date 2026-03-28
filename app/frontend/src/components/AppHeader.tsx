import { NavLink, useLocation } from "react-router-dom";
import { Logo } from "./Logo";

export function AppHeader() {
  const location = useLocation();
  const homeIsActive = location.pathname !== "/historico";

  return (
    <header className="site-header">
      <div className="header-content">
        <Logo />

        <nav className="main-nav" aria-label="Navegação principal">
          <NavLink
            className={`nav-link${homeIsActive ? " is-active" : ""}`}
            to="/"
          >
            Home
          </NavLink>
          <NavLink
            className={`nav-link${location.pathname === "/historico" ? " is-active" : ""}`}
            to="/historico"
          >
            Histórico
          </NavLink>
        </nav>
      </div>
    </header>
  );
}
