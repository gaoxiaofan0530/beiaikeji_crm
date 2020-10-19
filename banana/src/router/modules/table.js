/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const tableRouter = {
  path: '/table',
  component: Layout,
  redirect: '/table/complex-table',
  name: 'Table',
  meta: {
    title: '商机门店',
    icon: 'table'
  },
  children: [
    {
      path: 'complex-table',
      component: () => import('@/views/table/complex-table'),
      name: 'ComplexTable',
      meta: { title: '客户公海' }
    },
    {
      path: 'dynamic-table',
      component: () => import('@/views/table/drag-table'),
      name: 'DynamicTable',
      meta: { title: '个人私海' }
    }
    ,
    {
      path: 'drag-table',
      component: () => import('@/views/table/inline-edit-table'),
      name: 'DragTable',
      meta: { title: '拜访记录' }
    },
  ]
}
export default tableRouter
