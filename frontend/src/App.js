import React from "react";
import URLShortener from "./components/URLShortener";
import Header from "./components/Header";
import Footer from "./components/Footer";

function App() {
  return (
    <div className="App">
      <Header />
      <main style={{ minHeight: "calc(100vh - 140px)", padding: "2rem 0" }}>
        <URLShortener />
      </main>
      <Footer />
    </div>
  );
}

export default App;
