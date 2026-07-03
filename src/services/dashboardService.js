export async function getDashboard() {
  const res = await fetch('/api/dashboard')
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Failed to fetch dashboard: ${res.status} ${text}`)
  }
  return res.json()
}

export default { getDashboard }
