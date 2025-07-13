import React, { useState } from "react";
import {
  Copy,
  ExternalLink,
  AlertCircle,
  CheckCircle,
  Loader,
} from "lucide-react";
import axios from "axios";

const URLShortener = () => {
  const [url, setUrl] = useState("");
  const [shortUrl, setShortUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [copied, setCopied] = useState(false);

  const validateUrl = (url) => {
    try {
      new URL(url);
      return url.startsWith("http://") || url.startsWith("https://");
    } catch {
      return false;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!url.trim()) {
      setError("Please enter a URL");
      return;
    }

    if (!validateUrl(url)) {
      setError("Please enter a valid URL starting with http:// or https://");
      return;
    }

    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const response = await axios.post("/shorten", { url: url.trim() });
      setShortUrl(response.data.short_url);
      setSuccess("URL shortened successfully!");
      setUrl("");
    } catch (err) {
      if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else if (err.code === "ERR_NETWORK") {
        setError(
          "Unable to connect to server. Please make sure the backend is running on port 8000."
        );
      } else {
        setError("Failed to shorten URL. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(shortUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      // Fallback for older browsers
      const textArea = document.createElement("textarea");
      textArea.value = shortUrl;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand("copy");
      document.body.removeChild(textArea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const openUrl = () => {
    window.open(shortUrl, "_blank", "noopener,noreferrer");
  };

  return (
    <div className="container">
      <div style={{ maxWidth: "600px", margin: "0 auto" }}>
        {/* Main Card */}
        <div className="card fade-in">
          <div className="text-center mb-6">
            <h2
              style={{
                fontSize: "2rem",
                fontWeight: "700",
                marginBottom: "0.5rem",
                background: "#00E2DC",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
                backgroundClip: "text",
              }}
            >
              Shorten Your URLs
            </h2>
            <p style={{ color: "#6b7280", fontSize: "1.1rem" }}>
              Transform long URLs into short, shareable links in seconds
            </p>
          </div>

          {/* Error Alert */}
          {error && (
            <div className="alert alert-error scale-in">
              <AlertCircle size={20} />
              {error}
            </div>
          )}

          {/* Success Alert */}
          {success && (
            <div className="alert alert-success scale-in">
              <CheckCircle size={20} />
              {success}
            </div>
          )}

          {/* URL Input Form */}
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Enter your long URL here... (e.g., https://example.com/very/long/path)"
                className={`form-input ${error ? "error" : ""}`}
                disabled={loading}
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
              style={{ width: "100%" }}
            >
              {loading ? (
                <>
                  <Loader className="loading" size={20} />
                  Shortening...
                </>
              ) : (
                "Shorten URL"
              )}
            </button>
          </form>

          {/* Result Display */}
          {shortUrl && (
            <div className="mt-6 fade-in">
              <div
                style={{
                  background: "#f8fafc",
                  border: "2px solid #e2e8f0",
                  borderRadius: "0.5rem",
                  padding: "1rem",
                }}
              >
                <label
                  style={{
                    display: "block",
                    fontSize: "0.875rem",
                    fontWeight: "600",
                    color: "#374151",
                    marginBottom: "0.5rem",
                  }}
                >
                  Your shortened URL:
                </label>

                <div
                  style={{
                    display: "flex",
                    gap: "0.5rem",
                    alignItems: "center",
                    flexWrap: "wrap",
                  }}
                >
                  <input
                    type="text"
                    value={shortUrl}
                    readOnly
                    style={{
                      flex: "1",
                      padding: "0.75rem",
                      border: "1px solid #d1d5db",
                      borderRadius: "0.375rem",
                      background: "white",
                      fontSize: "0.875rem",
                      minWidth: "200px",
                    }}
                  />

                  <button
                    type="button"
                    onClick={copyToClipboard}
                    className={`btn ${
                      copied ? "btn-success" : "btn-secondary"
                    }`}
                    style={{ minWidth: "100px" }}
                  >
                    {copied ? (
                      <>
                        <CheckCircle size={16} />
                        Copied!
                      </>
                    ) : (
                      <>
                        <Copy size={16} />
                        Copy
                      </>
                    )}
                  </button>

                  <button
                    type="button"
                    onClick={openUrl}
                    className="btn btn-secondary"
                  >
                    <ExternalLink size={16} />
                    Test
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default URLShortener;
