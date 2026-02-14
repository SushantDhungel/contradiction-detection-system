interface Props {
  onFileSelect: (f: File | null) => void;
}

export default function VitalsUploadCard({ onFileSelect }: Props) {
  return (
    <div className="card">
      <h3>Upload Vitals (CSV)</h3>
      <input
        type="file"
        accept=".csv"
        onChange={(e) => onFileSelect(e.target.files?.[0] || null)}
      />
    </div>
  );
}
