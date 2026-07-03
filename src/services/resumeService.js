import api from './api'

export async function uploadResume(file, userId) {
  const fd = new FormData()
  fd.append('file', file)
  // user_id is automatically resolved from JWT token on the backend,
  // but we keep the parameter signature for compatibility.

  const res = await api.post('/resumes/upload', fd, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  return res.data
}

export default { uploadResume }
