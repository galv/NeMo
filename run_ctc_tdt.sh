# # Create a conda environment, activate it, then install via "./reinstall.sh" in top of NeMo directory.
# conda activate nemo-tdt-ctc

# # Download the data used by my workload.
# mkdir -p data_manifests
# python ./scripts/dataset_processing/get_librispeech_data.py --data_root data_manifests  --data_sets test_clean

# # Needed only for RNN-T and TDT models for maximum speed decoding
# pip install cuda-python


for model_name in nvidia/parakeet-tdt_ctc-1.1b nvidia/parakeet-tdt-1.1b; do

# nsys profile -c cudaProfilerApi \
    python examples/asr/speech_to_text_eval.py  pretrained_name=$model_name dataset_manifest=$(readlink -f data_manifests/test_clean.json)  batch_size=32  output_filename=test_clean_decoded.jsonl  amp=false  compute_dtype=bfloat16  use_cer=false num_workers=1 presort_manifest=true calculate_rtfx=true

done
