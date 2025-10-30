import type { MenuItem } from '~/types/navigation'

export const useNavigation = () => {
  const items: MenuItem[] = [
    { label: 'Home', to: '/' },
    { label: 'Posts', to: '/posts' },
    { label: 'About', to: '/about' }
  ]
  return items
}
