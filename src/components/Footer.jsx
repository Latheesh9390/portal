export default function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="bg-portal-navy text-white text-xs no-print">
      <div className="max-w-5xl mx-auto px-6 py-3 flex flex-col sm:flex-row justify-between gap-1">
        <span></span>
        <span></span>
      </div>
    </footer>
  );
}
