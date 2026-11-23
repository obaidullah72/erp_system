import { expect,it,vi } from 'vitest'
vi.mock('../../src/lib/axios',()=>({api:{get:vi.fn(),post:vi.fn(),patch:vi.fn()}}))
import { api } from '../../src/lib/axios'
import { serviceFor } from '../../src/services/resources'
import { resourceById } from '../../src/workspaces/catalog'
it('unavailable operations reject explicitly without sending guessed requests',async()=>{const service=serviceFor(resourceById['sales-invoices']);for(const operation of ['list','create','update','action','export'])await expect(service[operation]({})).rejects.toMatchObject({code:'capability_unavailable'});expect(api.get).not.toHaveBeenCalled();expect(api.post).not.toHaveBeenCalled()})
it('only sends supported foundation list filters',async()=>{api.get.mockResolvedValueOnce({data:{items:[],total:0}});await serviceFor(resourceById.users).list({q:'test',page:2,page_size:10,sort:'-name',business_id:'untrusted'});expect(api.get).toHaveBeenLastCalledWith('/users',{params:{q:'test',page:2,page_size:10},signal:undefined})})
it('loads direct details using the actual paginated list contract',async()=>{api.get.mockResolvedValueOnce({data:{items:[],total:101}}).mockResolvedValueOnce({data:{items:[{id:'found',name:'Actual user'}],total:101}});expect(await serviceFor(resourceById.users).get('found')).toMatchObject({name:'Actual user'});expect(api.get).toHaveBeenLastCalledWith('/users',{params:{page:2,page_size:100},signal:undefined})})
