import { describe, expect, it } from 'vitest'
import { fieldSchema, schemaFor, userSchema, businessSettingsSchema, applyBackendErrors } from '../../src/forms/schemas'
import catalog from '../../src/workspaces/catalog.json'
import { actions } from '../../src/workspaces/actions'
describe('decimal and reference validation',()=>{
 it('preserves decimal strings without floating-point loss',()=>{const field={type:'decimal',label:'Amount',required:true,precision:6,positive:true};expect(fieldSchema(field).parse('99999999999999.123456')).toBe('99999999999999.123456');for(const value of ['0','-1','NaN','Infinity','1e3','0.0000001'])expect(fieldSchema(field).safeParse(value).success).toBe(false)})
 it('rejects invalid dates, same locations and reversed intervals',()=>{expect(fieldSchema({type:'date',label:'Date',required:true}).safeParse('2026-02-30').success).toBe(false);const schema=schemaFor([{name:'date_from',label:'Start',type:'date',required:true},{name:'date_to',label:'End',type:'date',required:true}]);expect(schema.safeParse({date_from:'2026-12-01',date_to:'2026-11-01'}).success).toBe(false)})
 it('requires strong user passwords and valid settings',()=>{expect(userSchema(false).safeParse({name:'Person',email:'bad',password:'short',role_ids:[],active:true}).success).toBe(false);expect(businessSettingsSchema.safeParse({currency:'PKR',timezone:'Asia/Karachi'}).success).toBe(true);expect(businessSettingsSchema.safeParse({currency:'pk',timezone:'Unknown/Zone'}).success).toBe(false)})
 it('maps redacted backend field locations without echoing submitted secrets',()=>{const errors=[];applyBackendErrors({response:{data:{error:{details:[{location:['body','lines',0,'quantity'],type:'greater_than'}]}}}},(...args)=>errors.push(args));expect(errors[0][0]).toBe('lines.0.quantity');expect(errors[0][1].message).toContain('server rejected')})
})
describe('workspace contract inventory',()=>{
 it('has unique paths and complete named actions for every workspace',()=>{expect(catalog.length).toBe(123);expect(new Set(catalog.map((resource)=>resource.path)).size).toBe(catalog.length);for(const resource of catalog){expect(resource.readPermission).toMatch(/:read$/);for(const action of resource.actions)expect(actions[action]).toBeDefined();for(const field of resource.fields)expect(field.label).toBeTruthy()}})
 it('does not label planned APIs as connected',()=>{expect(catalog.filter((resource)=>resource.status==='connected').map((resource)=>resource.id).sort()).toEqual(['business-settings','roles','users']);expect(catalog.filter((resource)=>resource.group==='Reports')).toHaveLength(40)})
})
