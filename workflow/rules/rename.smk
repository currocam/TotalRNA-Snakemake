rule rename:
    output:
        expand(
            f"results/renamed_raw_reads/{{sample}}_{{read}}.fastq.gz",
            zip,
            sample=sample,
            read=read,
        ),
    log:
        "logs/renaming_files.log",
    conda:
        "../envs/base_python.yaml"
    benchmark:
        "benchmarks/renaming_files.log"
    script:
        "../scripts/rename_files.py"
