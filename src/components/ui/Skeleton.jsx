export function Skeleton({ className = 'h-4 bg-white/6 rounded-md', style = {} }) {
  return <div className={`${className} animate-pulse`} style={style} />
}

export default Skeleton
