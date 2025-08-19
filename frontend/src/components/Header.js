import React from "react";
import { Link } from "lucide-react";

const Header = () => {
  return (
    <header
      style={{
        background: "rgba(34, 116, 165, 0.8)",
        backdropFilter: "blur(10px)",
        borderBottom: "1px solid rgba(93, 211, 158, 0.3)",
      }}
    >
      <div className="container">
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: "1rem 0",
          }}
        >
          <Link size={28} style={{ color: "#F7F7FF", marginRight: "0.5rem" }} />
          <h1
            style={{
              color: "#F7F7FF",
              fontSize: "1.5rem",
              fontWeight: "700",
              margin: 0,
            }}
          >
            URL Shortener
          </h1>
        </div>
      </div>
    </header>
  );
};

export default Header;
