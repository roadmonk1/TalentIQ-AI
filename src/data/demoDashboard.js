export const demoDashboard = {
  user: {
    full_name: 'Aisha Khan',
    username: 'aisha.k',
    role: 'Student',
    profile_completion: 72,
  },
  scores: {
    careerScore: 81,
    resumeScore: 92,
    atsReadiness: 78,
    interviewReadiness: 68,
    breakdowns: {
      career: [
        { label: 'Skills', value: 32, weight: 0.4 },
        { label: 'Experience', value: 24, weight: 0.3 },
        { label: 'Visibility', value: 25, weight: 0.2 },
        { label: 'Network', value: 80, weight: 0.1 },
      ],
      resume: [
        { label: 'Keywords', value: 95, impact: 0.4 },
        { label: 'Structure', value: 88, impact: 0.3 },
        { label: 'Achievements', value: 80, impact: 0.3 },
      ],
      ats: [
        { label: 'Parsing', value: 82, impact: 0.5 },
        { label: 'Formatting', value: 72, impact: 0.3 },
        { label: 'Keywords match', value: 78, impact: 0.2 },
      ],
    },
  },
  skillGaps: [
    { skill: 'React', gap: 12 },
    { skill: 'System Design', gap: 28 },
    { skill: 'TypeScript', gap: 18 },
  ],
  ai: {
    recommendations: 3,
    insights: [
      { id: 1, text: 'Add 2-3 quantifiable achievements to your most recent role.', impact: 3 },
      { id: 2, text: 'Re-order skills to match job descriptions for Frontend roles.', impact: 2 },
      { id: 3, text: 'Practice behavioral answers for STAR format.', impact: 1 },
    ],
  },
  missions: {
    today: 'Polish your top project README and add metrics.',
    weeklyGoals: [
      { id: 1, title: 'Update Resume', progress: 0.8 },
      { id: 2, title: 'Mock Interview', progress: 0.45 },
    ],
  },
  activity: [
    { id: 1, text: 'ATS scan completed — Resume Score 92', time: '2h ago' },
    { id: 2, text: 'AI Mentor suggested: Add case study about migration', time: '1d ago' },
  ],
  interviews: [
    { id: 1, company: 'BrightHire', date: '2026-07-06', type: 'Phone' },
    { id: 2, company: 'Zephyr Labs', date: '2026-07-08', type: 'Onsite' },
  ],
  jobs: [
    { id: 1, title: 'Frontend Engineer', company: 'Arc Innovations', score: 92, why: 'Strong React and CSS skills; keywords match', missing_skills: ['TypeScript'] },
    { id: 2, title: 'Product Engineer', company: 'Nebula', score: 88, why: 'Product sense and roadmap experience; missing deep system-design examples', missing_skills: ['System Design'] },
    { id: 3, title: 'UI Engineer', company: 'Lumen', score: 86, why: 'Great visuals and component experience; need accessibility examples', missing_skills: ['Accessibility'] },
    { id: 4, title: 'Software Engineer', company: 'Orion', score: 84, why: 'Solid backend fundamentals but lower cloud certifications', missing_skills: ['Cloud (AWS)'] },
    { id: 5, title: 'Fullstack Developer', company: 'Helix', score: 81, why: 'Good fullstack fit but limited leadership examples', missing_skills: ['Leadership'] },
  ],
  timeline: [
    { id: 1, type: 'resume_analyzed', text: 'Resume analyzed — score 92', when: '2h ago' },
    { id: 2, type: 'career_score', text: 'Career score increased to 81', when: '1d ago' },
    { id: 3, type: 'job_matches', text: '5 new job matches found', when: '1d ago' },
    { id: 4, type: 'ai_mentor', text: 'AI Mentor added 3 recommendations', when: '2d ago' },
  ],
}
