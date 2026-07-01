import { Link, useNavigate } from "react-router-dom";

export default function Header() {
  const navigate = useNavigate();

  return (
    <header className="bg-white border-b-4 border-portal-navy no-print">
      <div className="max-w-5xl mx-auto px-6 py-4 flex items-center gap-4">
        
        <div className="text-center flex-1">
          <h1 className="text-portal-navy text-xl md:text-2xl font-bold leading-tight">
            Kuppam Engineering College (Autonomous)
          </h1>
          <p className="text-portal-blue text-sm">
            Chittoor, Andhra Pradesh, Pincode : 517425
          </p>
          <h2 className="text-portal-navy text-base md:text-lg font-semibold mt-1">
            KEC Examination Results Portal
          </h2>
        </div>
      </div>
      <nav className="bg-portal-navy text-white">
        <div className="max-w-5xl mx-auto px-6 flex gap-6 text-sm">
          <button
            onClick={() => navigate("/")}
            className="py-2 px-1 hover:text-portal-accent transition-colors"
          >
            Home
          </button>
      
        
          <Link to="/admin/login" className="py-2 px-1 hover:text-portal-accent transition-colors">
            Admin Login
          </Link>
        </div>
      </nav>
    </header>
  );
}
