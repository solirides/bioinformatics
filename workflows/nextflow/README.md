# PGIP Nextflow Pipelines

This directory houses reproducible workflow definitions used to ingest datasets, execute plugins, and benchmark annotations. The initial placeholder pipeline (`ingest_pangenome.nf`) demonstrates the expected structure.

## Running Locally

```bash
nextflow run ingest_pangenome.nf \
    --vcf data/example.vcf.gz \
    --gfa data/example.gfa \
    --reference data/reference.fa \
    --backend_api http://localhost:8000 \
    --publish_dir results/ingest
```

The pipeline now performs the following high-level steps using containerized tools:

1. **Normalize VCF** – `bcftools norm` (quay.io/biocontainers/bcftools) splits multiallelics, checks reference alleles, indexes, and captures summary statistics.
2. **Summarize VCF** – A lightweight process emits JSON metadata (record counts, timestamps) for downstream registration.
3. **Validate GFA** – `odgi stats` (quay.io/biocontainers/odgi) gathers structural metrics from the pangenome graph.
4. **Register Assets** – Placeholder `curl` step posts artifacts to the backend once the ingestion endpoint is implemented.

## Design Goals

- Use containerized processes with pinned digests
- Emit provenance metadata consumable by the backend
- Support both human and microbial pangenome ingestion
- Integrate with workflow registries (Dockstore, nf-core) when mature

Contributions that add richer QC, integrate authentication for asset registration, or replace placeholders with production-grade tooling are welcome.
