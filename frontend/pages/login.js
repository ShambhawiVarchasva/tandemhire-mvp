import { useState } from "react";
import Layout from "../components/Layout";
import Router from "next/router";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Login() {
  const [email, setEmail] = useState("");
  const [pw, setPw] = useState("");

  const register = async () => {
    const res = await fetch(`${API}/auth/register`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({email, password: pw, name: ""})
    });
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user_id", data.user_id);
      alert("Registered and logged in");
      Router.push("/candidate");
    } else {
      alert(JSON.stringify(data));
    }
  };

  const login = async () => {
    const res = await fetch(`${API}/auth/login`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({email, password: pw})
    });
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user_id", data.user_id);
      alert("Logged in");
      Router.push("/candidate");
    } else {
      alert(JSON.stringify(data));
    }
  };

  return (
    <Layout>
      <h2>Login / Register</h2>
      <input placeholder="email" value={email} onChange={e=>setEmail(e.target.value)} />
      <br />
      <input placeholder="password" type="password" value={pw} onChange={e=>setPw(e.target.value)} />
      <br />
      <button onClick={login}>Login</button>
      <button onClick={register}>Register</button>
    </Layout>
  );
}
