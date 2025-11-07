/**
 * Divisions Data
 * Organization divisions and specialized units
 */

export interface Division {
  id: string
  name: string
  category: string
  description: string
  image: string
  icon?: string
  hoverImage?: string
  slug: string
  longDescription?: string
  commander?: string
  memberCount?: number
  primaryShips?: string[]
  activities?: string[]
  established?: string
}

export const divisions: Division[] = [
  {
    id: '1',
    name: 'Combat Division',
    category: 'Military Operations',
    description: 'Elite combat wing specializing in tactical operations, fleet defense, and security missions across the verse.',
    image: '/assets/img/project/01.jpg',
    hoverImage: '/assets/img/project/hover-img.jpg',
    slug: 'combat-division',
    longDescription: 'Our Combat Division represents the backbone of organizational security. Comprised of skilled pilots and tacticians, this division handles everything from escort missions to large-scale fleet engagements. With state-of-the-art combat vessels and rigorous training protocols, we ensure the safety of all organizational assets.',
    commander: 'John "Striker" Morrison',
    memberCount: 45,
    primaryShips: ['Aegis Sabre', 'Anvil Hornet', 'Aegis Vanguard'],
    activities: ['Combat', 'Security', 'Escort'],
    established: '2947'
  },
  {
    id: '2',
    name: 'Exploration Division',
    category: 'Discovery & Mapping',
    description: 'Dedicated explorers charting unknown systems, discovering jump points, and surveying new territories for the organization.',
    image: '/assets/img/project/02.jpg',
    hoverImage: '/assets/img/project/hover-img.jpg',
    slug: 'exploration-division',
    longDescription: 'The Exploration Division pushes the boundaries of known space. Our explorers venture into uncharted territories, map new systems, and discover valuable resources. Equipped with long-range scanners and state-of-the-art navigation systems, we expand the frontiers of human knowledge.',
    commander: 'Elena "Navigator" Rodriguez',
    memberCount: 32,
    primaryShips: ['Anvil Carrack', 'Origin 600i Explorer', 'MISC Freelancer DUR'],
    activities: ['Exploration', 'Mapping', 'Discovery'],
    established: '2948'
  },
  {
    id: '3',
    name: 'Trading Division',
    category: 'Commerce & Economics',
    description: 'Commercial specialists managing trade routes, cargo operations, and economic ventures for organizational prosperity.',
    image: '/assets/img/project/03.jpg',
    hoverImage: '/assets/img/project/hover-img.jpg',
    slug: 'trading-division',
    longDescription: 'Our Trading Division drives the economic engine of the organization. Through strategic market analysis and efficient logistics, we maintain profitable trade routes across multiple systems. From bulk cargo hauling to specialized commodity trading, this division ensures our financial stability.',
    commander: 'David "Trader" Kim',
    memberCount: 38,
    primaryShips: ['MISC Hull C', 'Crusader Mercury Star Runner', 'Drake Caterpillar'],
    activities: ['Trading', 'Cargo', 'Commerce'],
    established: '2948'
  },
  {
    id: '4',
    name: 'Mining Division',
    category: 'Resource Extraction',
    description: 'Expert miners extracting valuable resources from asteroids and planetary surfaces to fuel organizational growth.',
    image: '/assets/img/project/04.jpg',
    hoverImage: '/assets/img/project/hover-img.jpg',
    slug: 'mining-division',
    longDescription: 'The Mining Division specializes in resource extraction operations. From asteroid mining to planetary surface operations, our miners locate and extract valuable materials. With advanced mining equipment and geological expertise, we supply resources for organizational and commercial needs.',
    commander: 'TBD',
    memberCount: 28,
    primaryShips: ['MISC Prospector', 'Argo MOLE', 'Orion'],
    activities: ['Mining', 'Resource Extraction', 'Refining'],
    established: '2949'
  },
  {
    id: '5',
    name: 'Medical Division',
    category: 'Healthcare & Rescue',
    description: 'Medical professionals providing emergency care, rescue operations, and medical support across all divisions.',
    image: '/assets/img/project/05.jpg',
    hoverImage: '/assets/img/project/hover-img.jpg',
    slug: 'medical-division',
    longDescription: 'Our Medical Division ensures the health and safety of all organizational members. Providing emergency medical services, search and rescue operations, and ongoing healthcare support, this division is always ready to respond. Equipped with medical ships and trained personnel, we save lives across the verse.',
    commander: 'Rachel "Doc" Williams',
    memberCount: 18,
    primaryShips: ['Cutlass Red', 'Apollo Medivac', 'Carrack Medical'],
    activities: ['Medical', 'Rescue', 'Emergency Response'],
    established: '2950'
  },
  {
    id: '6',
    name: 'Intelligence Division',
    category: 'Reconnaissance & Analysis',
    description: 'Intelligence specialists gathering data, analyzing threats, and providing strategic information for mission planning.',
    image: '/assets/img/project/06.jpg',
    hoverImage: '/assets/img/project/hover-img.jpg',
    slug: 'intelligence-division',
    longDescription: 'The Intelligence Division serves as our eyes and ears across the verse. Through reconnaissance missions, data analysis, and threat assessment, we provide critical information for all organizational operations. Our specialists use advanced sensors and intelligence-gathering techniques to keep us informed.',
    commander: 'Marcus "Wraith" Taylor',
    memberCount: 15,
    primaryShips: ['Aegis Sabre', 'Drake Herald', 'Origin 325a'],
    activities: ['Intelligence', 'Reconnaissance', 'Analysis'],
    established: '2949'
  }
]

/**
 * Get division by slug
 */
export function getDivisionBySlug(slug: string): Division | undefined {
  return divisions.find(division => division.slug === slug)
}

/**
 * Get divisions by category
 */
export function getDivisionsByCategory(category: string): Division[] {
  return divisions.filter(division => division.category === category)
}

/**
 * Get all division categories
 */
export function getDivisionCategories(): string[] {
  return Array.from(new Set(divisions.map(d => d.category)))
}
