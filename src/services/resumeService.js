export async function uploadResume(file, userId) {
  const fd = new FormData()
  fd.append('file', file)
  if (userId) fd.append('user_id', userId)

  const res = await fetch('/api/resumes/upload', {
    method: 'POST',
    body: fd,
  })

  const data = await res.json()
  if (!res.ok) throw new Error(data.reason || data.error || 'Upload failed')
  return data
}

export default { uploadResume }
