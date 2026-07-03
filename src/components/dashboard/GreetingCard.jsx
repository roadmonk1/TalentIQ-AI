import { motion } from 'framer-motion'
import Card from '../ui/Card'

export function GreetingCard({ user }) {
  return (
    <Card className="col-span-2" title={`Welcome back, ${user.full_name.split(' ')[0]}`}> 
      <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.08 }} className="text-slate-300">
        Here's your personalized mission control. Your AI Mentor has {user.recommendations} recommendations today.
      </motion.p>
    </Card>
  )
}

export default GreetingCard
