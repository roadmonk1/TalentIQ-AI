import { motion } from 'framer-motion'
import Card from '../ui/Card'

export function GreetingCard({ user }) {
  const fullName = user?.full_name || 'User'
  const firstName = fullName.split(' ')[0]
  const recommendationsCount = Array.isArray(user?.recommendations) ? user.recommendations.length : (user?.recommendations || 0)

  return (
    <Card className="col-span-2" title={`Welcome back, ${firstName}`}> 
      <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.08 }} className="text-slate-300">
        Here's your personalized mission control. Your AI Mentor has {recommendationsCount} recommendations today.
      </motion.p>
    </Card>
  )
}

export default GreetingCard
