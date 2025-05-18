import React, { useState } from "react";
import { GoogleLogin } from "@react-oauth/google";
import { ToastContainer, toast } from "react-toastify";
import { useNavigate } from "react-router-dom";

const Login = () => {
	const VITE_NODE_ENDPOINT = import.meta.env.VITE_NODE_ENDPOINT; // Backend endpoint
	const [loginInfo, setLoginInfo] = useState({
		email: "",
		password: "",
	});

	const navigate = useNavigate();

	const handleChange = (e) => {
		const { name, value } = e.target;
		setLoginInfo({ ...loginInfo, [name]: value });
	};

	const handleLogin = async (e) => {
		e.preventDefault();
		const { email, password } = loginInfo;

		if (!email || !password) {
			toast.error("Email and password are required!");
			return;
		}

		try {
			const response = await fetch(`${VITE_NODE_ENDPOINT}/api/auth/login`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(loginInfo),
			});

			const data = await response.json();
			if (data.success) {
				localStorage.setItem("token", data.jwtToken);
				localStorage.setItem("loggedInUser", data.name);
				localStorage.setItem("loggedInEmail", data.email); 
				toast.success("Login successful!");
				setTimeout(() => navigate("/dashboard"), 1000);
			}
			 else {
				toast.error(data.message || "Login failed!");
			}
		} catch (error) {
			toast.error("An error occurred during login.");
		}
	};

	// Google Login Success Handler
	const handleGoogleLogin = async (response) => {
		try {
			const { credential } = response; // Get Google credential (ID Token)

			// Send the token to the backend for verification
			const res = await fetch(`${VITE_NODE_ENDPOINT}/api/auth/google/login`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ token: credential }),
			});

			const data = await res.json();
			console.log("Google login response:", data);

			if (data.success) {
				localStorage.setItem("token", data.jwtToken);
				localStorage.setItem("loggedInUser", data.name);
				localStorage.setItem("loggedInEmail", data.email); 
				toast.success("Google login successful!");
				setTimeout(() => navigate("/dashboard"), 1000);
			} else {
				toast.error(data.message || "Google login failed!");
			}
		} catch (error) {
			toast.error("An error occurred during Google login.");
		}
	};

	return (
		<div className="container">
			<h1>Login</h1>
			<form onSubmit={handleLogin}>
				<div>
					<label htmlFor="email">Email</label>
					<input type="email" name="email" placeholder="Enter your email" value={loginInfo.email} onChange={handleChange} />
				</div>
				<div>
					<label htmlFor="password">Password</label>
					<input type="password" name="password" placeholder="Enter your password" value={loginInfo.password} onChange={handleChange} />
				</div>
				<button type="submit">Login</button>
			</form>

			{/* Google Login Button */}
			<div style={{ marginTop: "20px" }}>
				<GoogleLogin onSuccess={handleGoogleLogin} onError={() => toast.error("Google login failed!")} />
			</div>
			{/* Sign Up Link */}
			<div style={{ marginTop: "20px" }}>
				<p>
					Don't have an account?{" "}
					<span style={{ cursor: "pointer", color: "#007bff" }} onClick={() => navigate("/signup")}>
						Sign up here
					</span>
				</p>
			</div>
			<ToastContainer />
		</div>
	);
};

export default Login;
