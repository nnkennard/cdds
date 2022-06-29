#for conference_name in `ls data`
for conference_name in midl_2020
do
  echo $conference_name
  for forum in `ls data/$conference_name/parsed/`
  do
    echo $forum
    in_path="data/$conference_name/parsed/$forum/*"
    out_dir="data/$conference_name/$forum/parsed"
    mkdir -p $out_dir
    mv $in_path $out_dir
  done
done
