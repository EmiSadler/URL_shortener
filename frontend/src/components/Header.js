import React from "react";
import { Link } from "lucide-react";

const Header = () => {
  return (
    <header
      style={{
        background: "rgba(255, 255, 255, 0.1)",
        backdropFilter: "blur(10px)",
        borderBottom: "1px solid rgba(255, 255, 255, 0.2)",
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
          <Link size={28} style={{ color: "white", marginRight: "0.5rem" }} />
          <h1
            style={{
              color: "white",
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
