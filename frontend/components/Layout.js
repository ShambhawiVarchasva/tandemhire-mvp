export default function Layout({ children }) {
  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: 20 }}>
      <header style={{ marginBottom: 20 }}>
        <h1>TandemHire</h1>
      </header>
      <main>{children}</main>
    </div>
  );
}
