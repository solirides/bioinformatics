#!/usr/bin/env nextflow

/*
 * PGIP Nextflow pipeline: Ingest pangenome assets.
 *
 * This placeholder pipeline demonstrates how VCF and GFA assets could be
 * normalized and registered with the backend API. Future iterations will add
 * container images, real tools, and provenance reporting.
 */

nextflow.enable.dsl=2

params.vcf = params.vcf ?: "data/example.vcf.gz"
params.gfa = params.gfa ?: "data/example.gfa"
params.reference = params.reference ?: "data/reference.fa"
params.backend_api = params.backend_api ?: "http://localhost:8000"
params.publish_dir = params.publish_dir ?: "results/ingest"

process NORMALIZE_VCF {
    tag "vcf:${params.vcf}"
    publishDir params.publish_dir, mode: "copy", overwrite: true
    container "quay.io/biocontainers/bcftools:1.20--h8b25389_0"

    input:
    tuple path(vcf_file), path(reference)

    output:
    tuple path("normalized.vcf.gz"), path("normalized.vcf.gz.tbi"), path("normalized.vcf.stats")

    script:
    """
    bcftools norm -m-any --check-ref w -f ${reference} ${vcf_file} -Oz -o normalized.vcf.gz
    tabix -p vcf normalized.vcf.gz
    bcftools stats -s - normalized.vcf.gz > normalized.vcf.stats
    """
}

process SUMMARIZE_VCF {
    tag "summary:${params.vcf}"
    publishDir params.publish_dir, mode: "copy", pattern: "*.json", overwrite: true
    container "quay.io/biocontainers/jq:1.7--he0b1a49_1001"

    input:
    tuple path("normalized.vcf.gz"), path("normalized.vcf.gz.tbi"), path("normalized.vcf.stats")

    output:
    path "normalized.vcf.summary.json"

    script:
    """
    cat <<'JSON' | jq '.' > normalized.vcf.summary.json
    {
      "source": "${params.vcf}",
      "records": $(grep ^SN normalized.vcf.stats | awk '{s+=$4} END {print s+0}'),
      "ts": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    }
    JSON
    """
}

process VALIDATE_GFA {
    tag "gfa:${params.gfa}"
    publishDir params.publish_dir, mode: "copy", overwrite: true
    container "quay.io/biocontainers/odgi:0.8.5--h0033a41_1"

    input:
    path gfa_file

    output:
    path "gfa.stats.json"

    script:
    """
    odgi stats -i ${gfa_file} -S > gfa.stats.json
    """
}

process REGISTER_ASSETS {
    tag "register"
    container "curlimages/curl:8.9.1"

    input:
    tuple path(summary_json), path(gfa_stats)

    output:
    path "registration-response.json"

    script:
    """
    curl -sS -X POST \
      -H "Content-Type: application/json" \
      -d @${summary_json} \
      ${params.backend_api}/api/v1/assets/vcf > registration-response.json || true

    # Placeholder for future authenticated POST for GFA metadata
    """
}

workflow {
    Channel.fromPath(params.vcf).set { vcf_channel }
    Channel.fromPath(params.reference).set { reference_channel }
    Channel.fromPath(params.gfa).set { gfa_channel }

    vcf_with_ref = vcf_channel.combine(reference_channel)
    normalized = NORMALIZE_VCF(vcf_with_ref)
    summary = SUMMARIZE_VCF(normalized)
    gfa_stats = VALIDATE_GFA(gfa_channel)

    REGISTER_ASSETS(summary.combine(gfa_stats))

    summary.view { "VCF summary emitted: ${it}" }
    gfa_stats.view { "GFA stats emitted: ${it}" }
}
