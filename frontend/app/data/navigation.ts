/**
 * Navigation Menu Configuration
 * Main navigation structure for the site header
 * Only 6 main menu items as per requirements
 */

export interface NavigationItem {
  label: string
  path: string
  active?: boolean
}

export const mainNavigation: NavigationItem[] = [
  {
    label: 'Home',
    path: '/',
    active: false
  },
  {
    label: 'About',
    path: '/about',
    active: false
  },
  {
    label: 'Members',
    path: '/members',
    active: false
  },
  {
    label: 'Divisions',
    path: '/divisions',
    active: false
  },
  {
    label: 'Blog',
    path: '/blog',
    active: false
  },
  {
    label: 'Contact',
    path: '/contact',
    active: false
  }
]

/**
 * Helper function to set active state based on current route
 */
export function getNavigationWithActive(currentPath: string): NavigationItem[] {
  return mainNavigation.map(item => ({
    ...item,
    active: currentPath === item.path || currentPath.startsWith(item.path + '/')
  }))
}
