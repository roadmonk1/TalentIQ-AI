import { useState } from 'react'
import Card from './ui/Card'
import { uploadResume } from '../services/resumeService'

export default function UploadResume({ userId }) {
  const [open, setOpen] = useState(false)
  const [file, setFile] = useState(null)
  const [status, setStatus] = useState('idle')
  const [stages, setStages] = useState([])
  const [error, setError] = useState(null)

  const startUpload = async () => {
    if (!file) return
    setStatus('uploading')
    setError(null)
    setStages([{ stage: 'Uploading Resume', done: false }])
    try {
      const res = await uploadResume(file, userId)
      // show returned stages progressively
      const returned = res.stages || []
      // map to both top-level and detailed TalentParse substeps
      const detailed = []
      returned.forEach((s) => {
        detailed.push({ stage: s.stage })
        if (s.stage === 'Extracting') {
          detailed.push({ stage: 'Reading document' })
          detailed.push({ stage: 'Detecting sections' })
          detailed.push({ stage: 'Extracting contact information' })
          detailed.push({ stage: 'Extracting skills' })
          detailed.push({ stage: 'Extracting projects' })
          detailed.push({ stage: 'Extracting experience' })
        }
        if (s.stage === 'Analyzing') {
          detailed.push({ stage: 'Resume Health Analysis' })
        }
      })
      setStages(detailed)
      setStatus('done')
      // refresh dashboard to reflect processed resume
      setTimeout(() => window.location.reload(), 800)
    } catch (err) {
      setError(err.message)
      setStatus('error')
    }
  }

  return (
    <div>
      <button onClick={() => setOpen(true)} className="rounded-full bg-white/6 px-3 py-2 text-sm text-white">Upload resume</button>

      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="w-full max-w-2xl">
            <Card title="Upload Resume">
              <div className="space-y-4">
                <input onChange={(e) => setFile(e.target.files[0])} type="file" accept=".pdf,.docx" />
                <div className="flex items-center gap-2">
                  <button disabled={status === 'uploading'} onClick={startUpload} className="rounded-full bg-cyan-500/10 px-4 py-2 text-sm text-cyan-200">Start processing</button>
                  <button onClick={() => { setOpen(false); setStatus('idle'); setStages([]); setError(null) }} className="rounded-full bg-white/6 px-4 py-2 text-sm text-white">Close</button>
                </div>

                <div>
                  {status === 'uploading' && (
                    <div className="space-y-2">
                      <div className="text-sm text-slate-300">Processing resume…</div>
                      <ol className="list-decimal ml-5 text-sm">
                        {stages.length === 0 && <li>Starting…</li>}
                        {stages.map((s, idx) => (
                          <li key={idx} className="mt-1">{s.stage}</li>
                        ))}
                      </ol>
                    </div>
                  )}

                  {status === 'done' && (
                    <div className="text-sm text-emerald-300">Processing complete — dashboard will refresh shortly.</div>
                  )}

                  {status === 'error' && (
                    <div className="text-sm text-rose-400">Error: {error}</div>
                  )}
                </div>
              </div>
            </Card>
          </div>
        </div>
      )}
    </div>
  )
}
