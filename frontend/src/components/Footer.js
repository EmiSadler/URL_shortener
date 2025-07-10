import React from "react";
import { Heart, Github, ExternalLink } from "lucide-react";

const Footer = () => {
  return (
    <footer
      style={{
        background: "rgba(255, 255, 255, 0.1)",
        backdropFilter: "blur(10px)",
        borderTop: "1px solid rgba(255, 255, 255, 0.2)",
        color: "white",
        textAlign: "center",
        padding: "1rem 0",
      }}
    >
      <div className="container">
        <p
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "0.5rem",
            margin: 0,
            fontSize: "0.875rem",
          }}
        >
          Made with <Heart size={16} fill="currentColor" /> for{" "}
          <a
            href="https://picnic.io"
            target="_blank"
            rel="noopener noreferrer"
            style={{
              color: "white",
              textDecoration: "none",
              display: "inline-flex",
              alignItems: "center",
              gap: "0.25rem",
            }}
          >
            picnic.io
          </a>{" "}
          by Emily
          <a
            href="https://github.com/EmiSadler"
            target="_blank"
            rel="noopener noreferrer"
            style={{
              color: "white",
              marginLeft: "1rem",
              display: "flex",
              alignItems: "center",
              gap: "0.25rem",
              textDecoration: "none",
            }}
          >
            <Github size={16} /> View Code
          </a>
        </p>
      </div>
    </footer>
  );
};

export default Footer;
