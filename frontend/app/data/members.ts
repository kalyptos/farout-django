/**
 * Members Data
 * Organization member profiles and information
 */

export interface Member {
  id: string
  name: string
  handle?: string
  role: string
  rank?: string
  avatar: string
  description: string
  mainShip?: string
  activities?: string[]
  joinDate?: string
  slug: string
  bio?: string
  contactInfo?: {
    discord?: string
    email?: string
  }
}

export const members: Member[] = [
  {
    id: '1',
    name: 'John "Striker" Morrison',
    handle: 'Striker',
    role: 'Fleet Commander',
    rank: 'Admiral',
    avatar: '/assets/img/team/01.jpg',
    description: 'Leading our organization with strategic vision and tactical expertise. Specialized in combat operations and fleet coordination.',
    mainShip: 'Aegis Idris',
    activities: ['Combat', 'Leadership', 'Strategy'],
    joinDate: '2947',
    slug: 'john-morrison',
    bio: 'A veteran pilot with over 15 years of combat experience. John leads our organization with a focus on teamwork and strategic excellence.',
    contactInfo: {
      discord: 'Striker#1234'
    }
  },
  {
    id: '2',
    name: 'Sarah "Phoenix" Chen',
    handle: 'Phoenix',
    role: 'Operations Director',
    rank: 'Commander',
    avatar: '/assets/img/team/02.jpg',
    description: 'Coordinating all operational activities and mission planning. Expert in logistics and resource management.',
    mainShip: 'Anvil Carrack',
    activities: ['Exploration', 'Operations', 'Logistics'],
    joinDate: '2948',
    slug: 'sarah-chen',
    bio: 'Sarah brings exceptional organizational skills and exploration expertise to our team. She ensures every operation runs smoothly.',
    contactInfo: {
      discord: 'Phoenix#5678'
    }
  },
  {
    id: '3',
    name: 'Marcus "Wraith" Taylor',
    handle: 'Wraith',
    role: 'Security Chief',
    rank: 'Lieutenant',
    avatar: '/assets/img/team/03.jpg',
    description: 'Responsible for organization security and tactical training. Specialized in reconnaissance and stealth operations.',
    mainShip: 'Aegis Sabre',
    activities: ['Combat', 'Security', 'Recon'],
    joinDate: '2949',
    slug: 'marcus-taylor',
    bio: 'Marcus is a specialist in covert operations and threat assessment. His tactical expertise keeps our members safe.',
    contactInfo: {
      discord: 'Wraith#9012'
    }
  },
  {
    id: '4',
    name: 'Elena "Navigator" Rodriguez',
    handle: 'Navigator',
    role: 'Chief Explorer',
    rank: 'Commander',
    avatar: '/assets/img/team/04.jpg',
    description: 'Leading exploration missions and charting unknown territories. Expert cartographer and jump point specialist.',
    mainShip: 'Origin 600i Explorer',
    activities: ['Exploration', 'Mapping', 'Discovery'],
    joinDate: '2948',
    slug: 'elena-rodriguez',
    bio: 'Elena has discovered numerous jump points and surveyed countless systems. Her passion for exploration drives our discovery missions.',
    contactInfo: {
      discord: 'Navigator#3456'
    }
  },
  {
    id: '5',
    name: 'David "Trader" Kim',
    handle: 'Trader',
    role: 'Commerce Director',
    rank: 'Captain',
    avatar: '/assets/img/team/05.jpg',
    description: 'Managing all trading operations and economic activities. Specialist in market analysis and profitable trade routes.',
    mainShip: 'MISC Hull C',
    activities: ['Trading', 'Mining', 'Economy'],
    joinDate: '2949',
    slug: 'david-kim',
    bio: 'David expertise in commerce and market trends ensures our organization thrives economically. He negotiates the best deals across the verse.',
    contactInfo: {
      discord: 'Trader#7890'
    }
  },
  {
    id: '6',
    name: 'Rachel "Doc" Williams',
    handle: 'Doc',
    role: 'Medical Officer',
    rank: 'Lieutenant',
    avatar: '/assets/img/team/06.jpg',
    description: 'Providing medical support and rescue operations. Expert in emergency medicine and combat medic procedures.',
    mainShip: 'Cutlass Red',
    activities: ['Medical', 'Rescue', 'Support'],
    joinDate: '2950',
    slug: 'rachel-williams',
    bio: 'Rachel dedication to saving lives makes her an invaluable asset. She leads our medical division with compassion and expertise.',
    contactInfo: {
      discord: 'Doc#2345'
    }
  }
]

/**
 * Get member by slug
 */
export function getMemberBySlug(slug: string): Member | undefined {
  return members.find(member => member.slug === slug)
}

/**
 * Get members by activity
 */
export function getMembersByActivity(activity: string): Member[] {
  return members.filter(member =>
    member.activities?.includes(activity)
  )
}
