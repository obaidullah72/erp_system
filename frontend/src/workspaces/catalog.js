import definitions from './catalog.json'
export const resources = definitions
export const resourceById = Object.fromEntries(resources.map((resource) => [resource.id, resource]))
export const groups = ['Master data', 'Inventory', 'Purchases', 'Sales', 'Accounting', 'Manufacturing', 'Reports', 'Administration']
export const groupSlug = (name) => name.toLowerCase().replaceAll(' ', '-')
export const label = (value) => value.replaceAll('_', ' ').replace(/\b\w/g, (char) => char.toUpperCase())
