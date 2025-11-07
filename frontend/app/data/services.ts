import type { Service } from '~/types'

export const services: Service[] = [
  {
    id: '1',
    icon: '/assets/img/icon/01.svg',
    title: 'Combat Operations',
    description: 'Elite fighter pilots and tactical specialists ready for any combat scenario in the verse.',
    link: '/divisions/combat'
  },
  {
    id: '2',
    icon: '/assets/img/icon/03.svg',
    title: 'Exploration',
    description: 'Discover new systems, chart unexplored territories, and uncover hidden secrets of the universe.',
    link: '/divisions/exploration'
  },
  {
    id: '3',
    icon: '/assets/img/icon/04.svg',
    title: 'Trading & Commerce',
    description: 'Master traders running profitable trade routes across multiple systems and stations.',
    link: '/divisions/trading'
  },
  {
    id: '4',
    icon: '/assets/img/icon/05.svg',
    title: 'Mining Operations',
    description: 'Efficient mining crews extracting valuable resources from asteroids and planetary surfaces.',
    link: '/divisions/mining'
  },
  {
    id: '5',
    icon: '/assets/img/icon/06.svg',
    title: 'Intelligence',
    description: 'Information gathering, reconnaissance, and strategic analysis for all organizational operations.',
    link: '/divisions/intelligence'
  },
  {
    id: '6',
    icon: '/assets/img/icon/07.svg',
    title: 'Medical Corps',
    description: 'Medical professionals providing rescue, healthcare, and support services across all missions.',
    link: '/divisions/medical'
  }
]
