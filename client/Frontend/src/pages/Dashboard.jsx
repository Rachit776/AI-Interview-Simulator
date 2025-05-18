import { useEffect, useState } from "react";
import { FaChevronRight, FaCheck } from "react-icons/fa";
import { Link, useNavigate } from "react-router-dom";
import "./Dashboard.css";

const Dashboard = () => {
  const [selectedMenu, setSelectedMenu] = useState(null);
  const navigate = useNavigate();

  const menus = [
    "Frontend",
    "Backend",
    "DevOps",
    "Machine Learning",
    "System Design",
    "Graphic Design",
  ];

  // 🔐 Check token on load
  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/login"); // Redirect to login if no token
    }

    // Optionally: ping backend to verify token
    const verifyToken = async () => {
      try {
        const res = await fetch(`${import.meta.env.VITE_NODE_ENDPOINT}/auth/verify`, {
          headers: {
            "Authorization": `Bearer ${token}`,
          },
        });
        if (!res.ok) {
          // Token invalid or expired
          localStorage.removeItem("token");
          navigate("/login");
        }
      } catch (error) {
        console.error("Token verification failed:", error);
        navigate("/login");
      }
    };

    verifyToken();
  }, [navigate]);

  const handleMenuClick = (menu) => {
    setSelectedMenu(menu);
  };

  const getMenuRoute = (menu) => {
    switch (menu) {
      case "Frontend":
        return "/dashboard/frontend";
      case "Backend":
        return "/dashboard/backend";
      case "DevOps":
        return "/dashboard/devops";
      case "Machine Learning":
        return "/dashboard/machine-learning";
      case "System Design":
        return "/dashboard/system-design";
      case "Graphic Design":
        return "/dashboard/graphic-design";
      default:
        return "/dashboard";
    }
  };

  return (
    <div className="dashboard-content">
      <h2 className="header-text">Select to begin the interview process</h2>
      <div className="menu-container">
        {/* Menu Grid */}
        <div className="menu-grid">
          {menus.map((menu) => (
            <div
              key={menu}
              className={`menu-item ${selectedMenu === menu ? "selected" : ""}`}
              onClick={() => handleMenuClick(menu)}
            >
              {menu}
              {selectedMenu === menu && (
                <span className="tick">
                  <FaCheck />
                </span>
              )}
            </div>
          ))}
        </div>

        {/* Navigation Button */}
        <Link
          to={selectedMenu ? getMenuRoute(selectedMenu) : "#"}
          className={`next-button ${!selectedMenu ? "disabled" : ""}`}
        >
          Next <FaChevronRight />
        </Link>
      </div>
    </div>
  );
};

export default Dashboard;
