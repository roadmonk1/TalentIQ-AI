import sharedApi from './api'

function clientFor(api) {
  return api || sharedApi
}

export async function getMentorSession(api, sessionId) {
  const client = clientFor(api)
  const response = await client.get(`/mentor/session/${encodeURIComponent(sessionId)}`)
  return response.data
}

export async function getMentorContext(api, sessionId, userId) {
  const client = clientFor(api)
  const response = await client.get('/mentor/context', {
    params: {
      session_id: sessionId,
      user_id: userId,
    },
  })
  return response.data
}

export async function postMentorChat(api, payload) {
  const client = clientFor(api)
  const response = await client.post('/mentor/chat', payload)
  return response.data
}

export default {
  getMentorSession,
  getMentorContext,
  postMentorChat,
}
