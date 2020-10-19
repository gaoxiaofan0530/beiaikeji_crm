/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/layout'

const chartsRouter = {
  path: '/charts',
  component: Layout,
  redirect: 'noRedirect',
  name: 'Charts',
  meta: {
    title: '订单管理',
    icon: 'list'
  },
  children: [
    {
      path: '添加订单',
      component: () => import('@/views/charts/keyboard'),
      name: '添加订单',
      meta: { title: '创建订单', noCache: true }
    },
    {
      path: '我的订单',
      component: () => import('@/views/charts/line'),
      name: 'LineChart',
      meta: { title: '我的订单', noCache: true }
    },
    {
      path: '全部订单',
      component: () => import('@/views/charts/mix-chart'),
      name: 'LineChart',
      meta: { title: '全部订单', noCache: true }
    },
    {
      path: '审核订单',
      component: () => import('@/views/charts/shenhe_order'),
      name: 'LineChart',
      meta: { title: '审核订单', noCache: true }
    }
  ]
}

export default chartsRouter
