import maya.cmds as cmds

def mirror_constraints():

    print("\n--------------------------------------------------")
    print("# CONSTRAINT")
    print("--------------------------------------------------")

    all_constraints = [i for i in cmds.ls(type='constraint') if i.startswith('l_')]
    axes = {'X', 'Y', 'Z'}

    def replace_prefix(item):
        return item.replace('l_', 'r_', 1)

    for constr in all_constraints:
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
            mirrored_driver_list = [replace_prefix(i) for i in driver_list] or []
            mirrored_driven = replace_prefix(driven_obj) or []

            if not mirrored_driver_list:
                print('No driver found')
            if not mirrored_driver_list:
                print('No driver found')

            # Check if there're skip axes and create parentConstraint
            if not skipped_translate:
                skipped_translate = ['none']
            if not skipped_rotate:
                skipped_rotate = ['none']

            mirrored_constraint = cmds.parentConstraint(mirrored_driver_list, mirrored_driven, st=skipped_translate, sr=skipped_rotate, mo=True)

            print(f"- {mirrored_constraint[0]}")
            print(f"    - driver: {', '.join(mirrored_driver_list)}")
            print(f"    - driven: {mirrored_driven}")
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
            mirrored_driver_list = [replace_prefix(i) for i in driver_list] or []
            mirrored_driven = replace_prefix(driven_obj) or []

            if not mirrored_driver_list:
                print('No driver found')
            if not mirrored_driver_list:
                print('No driver found')

            # Check if there're skip axes and create parentConstraint
            if not skipped_scale:
                skipped_scale = ['none']

            mirrored_constraint = cmds.scaleConstraint(mirrored_driver_list, mirrored_driven, sk=skipped_scale, mo=True)

            print(f"- {mirrored_constraint[0]}")
            print(f"    - driver: {', '.join(mirrored_driver_list)}")
            print(f"    - driven: {mirrored_driven}")
            print(f"    - skipped_scale: {', '.join(skipped_scale)}")


        elif constraint_type == 'pointConstraint':
            driver_list = cmds.pointConstraint(constr, q=True, tl=True)

            for i in axes:
                s_driven = cmds.listConnections(f'{constr}.constraintScale{i}', s=False, d=True) or []
                drivens_on_axis += s_driven
                if not s_driven:
                    skipped_translate += i.lower()

            # Get the driven object
            driven_obj = list(set(drivens_on_axis))
            if len(driven_obj) == 1:
                driven_obj = driven_obj[0]
            else:
                cmds.warning(f'More than one driven obj: {driven_obj}')

            # Mirror driver and driven
            mirrored_driver_list = [replace_prefix(i) for i in driver_list] or []
            mirrored_driven = replace_prefix(driven_obj) or []

            if not mirrored_driver_list:
                print('No driver found')
            if not mirrored_driver_list:
                print('No driver found')

            # Check if there're skip axes and create parentConstraint
            if not skipped_translate:
                skipped_translate = ['none']

            mirrored_constraint = cmds.pointConstraint(mirrored_driver_list, mirrored_driven, sk=skipped_translate, mo=True)

            print(f"- {mirrored_constraint[0]}")
            print(f"    - driver: {', '.join(mirrored_driver_list)}")
            print(f"    - driven: {mirrored_driven}")
            print(f"    - skipped_translate: {', '.join(skipped_translate)}")


        elif constraint_type == 'rotateConstraint':
            driver_list = cmds.rotateConstraint(constr, q=True, tl=True)

            for i in axes:
                s_driven = cmds.listConnections(f'{constr}.constraintScale{i}', s=False, d=True) or []
                drivens_on_axis += s_driven
                if not s_driven:
                    skipped_rotate += i.lower()

            # Get the driven object
            driven_obj = list(set(drivens_on_axis))
            if len(driven_obj) == 1:
                driven_obj = driven_obj[0]
            else:
                cmds.warning(f'More than one driven obj: {driven_obj}')

            # Mirror driver and driven
            mirrored_driver_list = [replace_prefix(i) for i in driver_list] or []
            mirrored_driven = replace_prefix(driven_obj) or []

            if not mirrored_driver_list:
                print('No driver found')
            if not mirrored_driver_list:
                print('No driver found')

            # Check if there're skip axes and create parentConstraint
            if not skipped_rotate:
                skipped_rotate = ['none']

            mirrored_constraint = cmds.rotateConstraint(mirrored_driver_list, mirrored_driven, sk=skipped_rotate, mo=True)

            print(f"- {mirrored_constraint[0]}")
            print(f"    - driver: {', '.join(mirrored_driver_list)}")
            print(f"    - driven: {mirrored_driven}")
            print(f"    - skipped_rotate: {', '.join(skipped_rotate)}")

# mirror_constraints()
