export HUSKY_DESCRIPTION=$(catkin_find --first-only --without-underlays husky_custom_description urdf/custom_description.urdf.xacro 2>/dev/null)
export HUSKY_DESCRIPTION_WATER_TANK=$(catkin_find --first-only --without-underlays husky_custom_description urdf/custom_water_tank.urdf.xacro 2>/dev/null)
