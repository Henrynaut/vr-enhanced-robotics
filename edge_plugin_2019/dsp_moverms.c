#include <math.h>
#include <string.h>
#include "dsp.h"
#include "doug.h"

DSS_NODE *shp_node;
DSS_NODE *elp_node;
int shp_id;
int elp_id;
float tgt_shp_angle = 25.0 ;
float tgt_elp_angle = -25.0;
 
/* Updates SHP and ELP angles in scene.  This example assumes the arm is iniatially in
 * rest position in the payload bay.  It raises the upper arm but leaves the lower arm
 * level with the payload bay.  Hence, both SHP and ELP need to be updated.
 */
void UpdateRMS()
{
	float shp_angle ;
	float elp_angle ;
	double next_time ;

	// Locks scene
	DSF_BgnModifyScene( DSV_scene );

	// Gets current time and angles
	next_time = DSF_GetSeconds();
	shp_angle = shp_node->P;
	elp_angle = elp_node->P;

	// If current SHP is less than target angle
	if ( shp_angle < tgt_shp_angle || elp_angle > tgt_elp_angle )
	{
		// Update SHP and ELP every .01 second
		if ( DSF_GetSeconds() >= next_time )
		{
			shp_angle += .01 ;
			if ( shp_angle > tgt_shp_angle ) shp_angle = tgt_shp_angle ;
			shp_node->P = shp_angle;

			elp_angle -= .01 ;
			if ( elp_angle < tgt_elp_angle ) elp_angle = tgt_elp_angle ;
      
     			elp_node->P = elp_angle;

			next_time += 0.01 ;
		}
	}

	// Notify scene of updated node
	DSF_ModifiedNode( shp_id, DSD_PYR_MODIFIED );
	DSF_ModifiedNode( elp_id, DSD_PYR_MODIFIED );

	// Unlock scene
	DSF_EndModifyScene( DSV_scene );

	// Execute rest of UPDATE_SCENE functional module
	DSF_ExecuteCore();
}

/* Initialize variables and install plugin function */
DSP_InitializePlugin( DSS_PLUGIN *plugin )
{
	int i;

	shp_id = DSF_GetNodeID( "SHP" ) ;
	elp_id = DSF_GetNodeID( "ELP" ) ;

	shp_node = DSV_scene->node_list + shp_id;
	elp_node = DSV_scene->node_list + elp_id;

	// Install plugin function – UpdateRMS – in UPDATE_SCENE functional module
	DSF_InstallPluginFunction( plugin->handle, UpdateRMS, DSD_PLUGIN_UPDATE_SCENE );

	return 1;
}

/* Cleanup function upon unloading plugin */
DSP_CleanupPlugin( DSS_PLUGIN *plugin )
{
}

/* Cleanup function upon exiting DOUG */
DSP_ExitPlugin( DSS_PLUGIN *plugin )
{
}

