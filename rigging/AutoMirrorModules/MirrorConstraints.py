import maya.cmds as cmds
import importlib

AutoMirror = importlib.import_module('OgravMaya.rigging.AutoMirror')
# importlib.reload(AutoMirror)

all_attrs = AutoMirror.get_attrs()
src = all_attrs['src']
mir = all_attrs['mir']
ctrl_suffix = all_attrs['ctrl_suffix']
mirror_axis = all_attrs['mirror_axis']

def main():

    print("\n--------------------------------------------------")
    print("# CONSTRAINT")
    print("--------------------------------------------------")

    axes = {'X', 'Y', 'Z'}

    all_src_constraints = [i for i in cmds.ls(type='constraint') if i.startswith(src)]

    if not all_src_constraints:
        print("No source constraints found")
        return

    all_mir_constraints = [i.replace(src, mir, 1) for i in all_src_constraints]
    update_existing_mirrored_constraints(all_mir_constraints)

    def replace_prefix(item):
        return item.replace(src, mir, 1)


    for constr in all_src_constraints:
        # constraint_type = constr.split('_')[-1][0:-1] # e.g. l_cube_parentConstraint1
        constraint_type = cmds.objectType(constr)

        drivens_on_axis = []
        skipped_translate, skipped_rotate, skipped_scale = [], [], []

        if constraint_type == 'parentConstraint':
            driver_list = cmds.parentConstraint(constr, q=True, tl=True)

            for i in axes:
                t_driven = cmds.listConnections(f'{constr}.constraintTranslate{i}', s=False, d=True) or []
                drivens_on_axis += t_driven
                if not t_driven:
                    skipped_translate += i.lower()

                r_driven = cmds.listConnections(f'{constr}.constraintRotate{i}', s=False, d=True) or []
                drivens_on_axis += r_driven
                if not r_driven:
                    skipped_rotate += i.lower()

            # Get the driven object
            driven_obj = list(set(drivens_on_axis))
            if len(driven_obj) == 1:
                driven_obj = driven_obj[0]
            else:
                cmds.warning(f'More than one driven obj: {driven_obj}')

            # Mirror driver and driven
            mir_driver_list = [replace_prefix(i) for i in driver_list] or []
            mir_driven = replace_prefix(driven_obj) or ''


            # Check if there're skip axes and create parentConstraint
            if not skipped_translate:
                skipped_translate = ['none']
            if not skipped_rotate:
                skipped_rotate = ['none']

            mir_constraint = cmds.parentConstraint(mir_driver_list, mir_driven, st=skipped_translate, sr=skipped_rotate, mo=True)

            print(f"- {mir_constraint[0]}")
            print(f"    - driver: {', '.join(mir_driver_list)}")
            print(f"    - driven: {mir_driven}")
            print(f"    - skipped_translate: {', '.join(skipped_translate)}")
            print(f"    - skipped_rotate: {', '.join(skipped_rotate)}")


        elif constraint_type == 'scaleConstraint':
            driver_list = cmds.scaleConstraint(constr, q=True, tl=True)

            for i in axes:
                s_driven = cmds.listConnections(f'{constr}.constraintScale{i}', s=False, d=True) or []
                drivens_on_axis += s_driven
                if not s_driven:
                    skipped_scale += i.lower()

            # Get the driven object
            driven_obj = list(set(drivens_on_axis))
            if len(driven_obj) == 1:
                driven_obj = driven_obj[0]
            else:
                cmds.warning(f'More than one driven obj: {driven_obj}')

            # Mirror driver and driven
            mir_driver_list = [replace_prefix(i) for i in driver_list] or []
            mir_driven = replace_prefix(driven_obj) or ''


            # Check if there're skip axes and create parentConstraint
            if not skipped_scale:
                skipped_scale = ['none']

            mir_constraint = cmds.scaleConstraint(mir_driver_list, mir_driven, sk=skipped_scale, mo=True)

            print(f"- {mir_constraint[0]}")
            print(f"    - driver: {', '.join(mir_driver_list)}")
            print(f"    - driven: {mir_driven}")
            print(f"    - skipped_scale: {', '.join(skipped_scale)}")


        elif constraint_type == 'pointConstraint':
            driver_list = cmds.pointConstraint(constr, q=True, tl=True)

            for i in axes:
                t_driven = cmds.listConnections(f'{constr}.constraintTranslate{i}', s=False, d=True) or []
                drivens_on_axis += t_driven
                if not t_driven:
                    skipped_translate += i.lower()

            # Get the driven object
            driven_obj = list(set(drivens_on_axis))
            if len(driven_obj) == 1:
                driven_obj = driven_obj[0]
            else:
                cmds.warning(f'More than one driven obj: {driven_obj} in src constraint: {constr}')

            # Mirror driver and driven
            mir_driver_list = [replace_prefix(i) for i in driver_list] or []
            mir_driven = replace_prefix(driven_obj) or ''

            # Check if there're skip axes and create parentConstraint
            if not skipped_translate:
                skipped_translate = ['none']

            mir_constraint = cmds.pointConstraint(mir_driver_list, mir_driven, sk=skipped_translate, mo=True)

            print(f"- {mir_constraint[0]}")
            print(f"    - driver: {', '.join(mir_driver_list)}")
            print(f"    - driven: {mir_driven}")
            print(f"    - skipped_translate: {', '.join(skipped_translate)}")


        elif constraint_type == 'rotateConstraint':
            driver_list = cmds.rotateConstraint(constr, q=True, tl=True)

            for i in axes:
                r_driven = cmds.listConnections(f'{constr}.constraintRotate{i}', s=False, d=True) or []
                drivens_on_axis += r_driven
                if not r_driven:
                    skipped_rotate += i.lower()

            # Get the driven object
            driven_obj = list(set(drivens_on_axis))
            if len(driven_obj) == 1:
                driven_obj = driven_obj[0]
            else:
                cmds.warning(f'More than one driven obj: {driven_obj}')

            # Mirror driver and driven
            mir_driver_list = [replace_prefix(i) for i in driver_list] or []
            mir_driven = replace_prefix(driven_obj) or ''

            # Check if there're skip axes and create parentConstraint
            if not skipped_rotate:
                skipped_rotate = ['none']

            mir_constraint = cmds.rotateConstraint(mir_driver_list, mir_driven, sk=skipped_rotate, mo=True)

            print(f"- {mir_constraint[0]}")
            print(f"    - driver: {', '.join(mir_driver_list)}")
            print(f"    - driven: {mir_driven}")
            print(f"    - skipped_rotate: {', '.join(skipped_rotate)}")


        elif constraint_type == 'aimConstraint':
            driver_list = cmds.aimConstraint(constr, q=True, tl=True)
            aim_vector = cmds.aimConstraint(constr, q=True, aimVector=True)
            up_vector = cmds.aimConstraint(constr, q=True, upVector=True)
            world_up_type = cmds.aimConstraint(constr, q=True, worldUpType=True)
            world_up_vector = cmds.aimConstraint(constr, q=True, worldUpVector=True)
            world_up_obj = cmds.aimConstraint(constr, q=True, worldUpObject=True)[0]

            for i in axes:
                r_driven = cmds.listConnections(f'{constr}.constraintRotate{i}', s=False, d=True) or []
                drivens_on_axis += r_driven
                if not r_driven:
                    skipped_rotate += i.lower()

            # Check if there're skip axes and create parentConstraint
            if not skipped_rotate:
                skipped_rotate = ['none']

            # Get the driven object
            driven_obj = list(set(drivens_on_axis))
            if len(driven_obj) == 1:
                driven_obj = driven_obj[0]
            else:
                cmds.warning(f'More than one driven obj: {driven_obj}')

            # Mirror driver and driven
            mir_driver_list = [replace_prefix(i) for i in driver_list] or []
            mir_driven = replace_prefix(driven_obj) or ''

            # Mirror the world up obj if it's on the src side
            if world_up_obj.startswith(src):
                world_up_obj = replace_prefix(world_up_obj)

            mir_constraint = cmds.aimConstraint(mir_driver_list, mir_driven, sk=skipped_rotate, mo=True, aimVector=aim_vector, upVector=up_vector, worldUpType=world_up_type, worldUpVector=world_up_vector, worldUpObject=world_up_obj)

            print(f"- {mir_constraint[0]}")
            print(f"    - driver: {', '.join(mir_driver_list)}")
            print(f"    - driven: {mir_driven}")
            print(f"    - skipped_axes: {', '.join(skipped_rotate)}")


        elif constraint_type == 'poleVectorConstraint':
            driver_list = cmds.poleVectorConstraint(constr, q=True, tl=True)

            for i in axes:
                t_driven = cmds.listConnections(f'{constr}.constraintTranslate{i}', s=False, d=True) or []
                drivens_on_axis += t_driven

            # Get the driven object
            driven_obj = list(set(drivens_on_axis))
            if len(driven_obj) == 1:
                driven_obj = driven_obj[0]
            else:
                cmds.warning(f'More than one driven obj: {driven_obj}')

            # Mirror driver and driven
            mir_driver_list = [replace_prefix(i) for i in driver_list] or []
            mir_driven = replace_prefix(driven_obj) or ''

            mir_constraint = cmds.poleVectorConstraint(mir_driver_list, mir_driven)

            print(f"- {mir_constraint[0]}")
            print(f"    - driver: {', '.join(mir_driver_list)}")
            print(f"    - driven: {mir_driven}")



    cmds.select(cl=True)


def update_existing_mirrored_constraints(items):
    for i in items: 
        if cmds.objExists(i):
            cmds.delete(i)
            print(f"Updated existing mirrored constraints: {i}")


# main()