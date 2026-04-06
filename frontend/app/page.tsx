"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [rates, setRates] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [limit] = useState(10);
  const [total, setTotal] = useState(0);
  const [pages, setPages] = useState(0);
  const [search, setSearch] = useState("");

  const fetchRates = async (pageNum: number = 1, searchTerm: string = "") => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const params = new URLSearchParams({
        page: pageNum.toString(),
        limit: limit.toString(),
        ...(searchTerm && { search: searchTerm })
      });

      const res = await fetch(`${apiUrl}/api/rates/history?${params}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (!res.ok) {
        throw new Error(`API error: ${res.status}`);
      }
      const data = await res.json();
      setRates(data.results);
      setTotal(data.total);
      setPages(data.pages);
      setPage(pageNum);
    } catch (err) {
      console.error("Error fetching rates:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRates(1, search);
  }, [search]);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
    setPage(1);
  };

  const handlePageChange = (newPage: number) => {
    if (newPage > 0 && newPage <= pages) {
      fetchRates(newPage, search);
    }
  };

  if (loading) return <p style={{ color: "var(--foreground)" }}>Loading data...</p>;

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif", color: "var(--foreground)" }}>
      <h1 style={{ color: "var(--foreground)" }}> Rate Dashboard</h1>

      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Search by provider or rate type..."
          value={search}
          onChange={handleSearch}
          style={{
            padding: "8px 12px",
            fontSize: "14px",
            width: "300px",
            borderRadius: "4px",
            border: "1px solid var(--border-color)",
            backgroundColor: "var(--background)",
            color: "var(--foreground)"
          }}
        />
      </div>

      <table border={1} cellPadding={10} style={{ width: "100%", borderCollapse: "collapse", borderColor: "var(--table-border)" }}>
        <thead>
          <tr style={{ backgroundColor: "var(--header-bg)", color: "var(--foreground)" }}>
            <th>Provider</th>
            <th>Rate Type</th>
            <th>Rate</th>
            <th>Date</th>
            <th>Currency</th>
          </tr>
        </thead>

        <tbody>
          {rates.length === 0 ? (
            <tr>
              <td colSpan={5} style={{ textAlign: "center", padding: "20px", color: "var(--foreground)" }}>
                No data found
              </td>
            </tr>
          ) : (
            rates.map((r, i) => (
              <tr key={i} style={{ borderBottom: "1px solid var(--table-border)", color: "var(--foreground)" }}>
                <td>{r.provider}</td>
                <td>{r.rate_type}</td>
                <td>{r.rate_value}</td>
                <td>{r.effective_date}</td>
                <td>{r.currency}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>

      <div style={{ marginTop: "20px", display: "flex", gap: "10px", alignItems: "center", color: "var(--foreground)" }}>
        <button
          onClick={() => handlePageChange(page - 1)}
          disabled={page === 1}
          style={{
            padding: "8px 12px",
            cursor: page === 1 ? "not-allowed" : "pointer",
            opacity: page === 1 ? 0.5 : 1,
            backgroundColor: "var(--header-bg)",
            color: "var(--foreground)",
            border: "1px solid var(--border-color)"
          }}
        >
          Previous
        </button>

        <span style={{ color: "var(--foreground)" }}>
          Page {page} of {pages} | Total: {total} records
        </span>

        <button
          onClick={() => handlePageChange(page + 1)}
          disabled={page === pages}
          style={{
            padding: "8px 12px",
            cursor: page === pages ? "not-allowed" : "pointer",
            opacity: page === pages ? 0.5 : 1,
            backgroundColor: "var(--header-bg)",
            color: "var(--foreground)",
            border: "1px solid var(--border-color)"
          }}
        >
          Next
        </button>
      </div>
    </div>
  );
}