import React from "react";
import { Heart, Github, ExternalLink } from "lucide-react";

const Footer = () => {
  return (
    <footer
      style={{
        background: "rgba(34, 116, 165, 0.8)",
        backdropFilter: "blur(10px)",
        borderTop: "1px solid rgba(93, 211, 158, 0.3)",
        color: "#F7F7FF",
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
          Made with <Heart size={16} fill="currentColor" />
          by Emily
          <a
            href="https://github.com/EmiSadler/URL_shortener"
            target="_blank"
            rel="noopener noreferrer"
            style={{
              color: "#F7F7FF",
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
