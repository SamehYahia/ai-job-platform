{{- define "ai-job-platform.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "ai-job-platform.fullname" -}}
{{- printf "%s-%s" .Release.Name (include "ai-job-platform.name" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "ai-job-platform.labels" -}}
app.kubernetes.io/name: {{ include "ai-job-platform.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version }}
{{- end }}

{{- define "ai-job-platform.selectorLabels" -}}
app.kubernetes.io/name: {{ include "ai-job-platform.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
{{- define "ai-job-platform.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "ai-job-platform.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}