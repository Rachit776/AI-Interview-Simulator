import { useEffect, useState } from "react";
import { jsPDF } from "jspdf";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./Profile.css";

const Profile = () => {
	const [userData, setUserData] = useState({ username: "", email: "" });
	const [profileImage, setProfileImage] = useState(null);
	const DEFAULT_AVATAR = "https://mcdn.wallpapersafari.com/medium/95/19/uFaSYI.jpg";

	useEffect(() => {
		// Fetch user data (replace with API call if needed)
		const storedUsername = localStorage.getItem("loggedInUser") || "Guest";
		const storedUseremail = localStorage.getItem("loggedInEmail") || "NA";
		const storedProfileImage = localStorage.getItem(`profileImage_${storedUseremail}`); 
		setUserData({ username: storedUsername, email: storedUseremail });
		setProfileImage(storedProfileImage || DEFAULT_AVATAR);
		
	}, []);

	// Handle profile picture upload
	const handleImageUpload = (e) => {
		const file = e.target.files[0];
		if (file && userData.email) {
			const reader = new FileReader();
			reader.onloadend = () => {
				setProfileImage(reader.result);
				localStorage.setItem(`profileImage_${userData.email}`, reader.result); 
			};
			reader.readAsDataURL(file);
		}
	};

	return (
		<div className="profile-container">
			<ToastContainer position="top-right" autoClose={3000} hideProgressBar />
			<div className="profile-card">
				{/* Left Side */}
				<div className="left-side">
					<div className="avatar-container">
						<label htmlFor="profile-upload" className="upload-label">
							<img src={profileImage || "https://via.placeholder.com/150?text=Upload"} alt="Profile Avatar" className="profile-avatar" />
						</label>
						<input type="file" id="profile-upload" style={{ display: "none" }} onChange={handleImageUpload} accept="image/*" />
					</div>
					<h3>Candidate Profile</h3>
					<div className="user-details">
						<p>
							<strong>Username:</strong> {userData.username}
						</p>
						<p>
							<strong>Email:</strong> {userData.email}
						</p>
					</div>
				</div>
			</div>
		</div>
	);
};

export default Profile;
