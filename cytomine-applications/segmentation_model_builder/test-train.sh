#Example to run a segmentation model builder

#1. Edit add_software.py and add the software to your Cytomine project if not existing yet


#2. Edit following XXX and 0 values with your cytomine identifiers
host="XXX"
software=0
public_key="XXX"
private_key="XXX"
id_project=0
working_path=XXX #e.g. /bigdata/tmp/cytomine/
annotation_projects=0 #separated by ,
predict_terms=0 #id of terms to be grouped into the positive class (e.g. tumor) separated by ,
excluded_terms=0 #id of terms that will not be used (neither positive nor negative class) separated by ,
model_file=XXX.pkl #filename of the segmentation model that will be created in $working_path/models/$model_file

#3. Edit pyxit parameter values to build segmentation model
zoom=0 #zoom level to extract annotations (0 = maximum resolution)
windowsize=24 #size of fixed-size subwindows
colorspace=2 #colorspace to encode pixel values
njobs=10 #number of parallel threads
interpolation=1 #interpolation (not used)
nbt=10 #number of trees
k=28 #number of tests evaluated in each internal tree node
nmin=10 #minimum node sample size
subw=100 #number of subwindows extracted by annotation crop


#4. Run
#Note: 
#-Annotations will be dumped into $working_path/$id_project/zoom_level/$zoom/...
#-Model will be created into $working_path/models/$model_file
#-If you want to use only reviewed annotations, uncomment --cytomine_reviewed
python add_and_run_job.py --cytomine_host $host --cytomine_public_key $public_key --cytomine_private_key $private_key --cytomine_base_path /api/ --cytomine_id_software $software --cytomine_working_path $working_path --cytomine_id_project $id_project --cytomine_annotation_projects $annotation_projects  -z $zoom --cytomine_predict_terms $predict_terms --cytomine_excluded_terms $excluded_terms --pyxit_target_width $windowsize --pyxit_target_height $windowsize --pyxit_colorspace $colorspace --pyxit_n_jobs $njobs --pyxit_save_to $working_path/models/$model_file --pyxit_transpose --pyxit_fixed_size --pyxit_interpolation $interpolation --forest_n_estimators $nbt --forest_max_features $k --forest_min_samples_split $nmin --pyxit_n_subwindows $subw --verbose #--cytomine_reviewed
