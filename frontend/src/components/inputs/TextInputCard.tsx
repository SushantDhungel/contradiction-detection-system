interface Props {
  value: string;
  onChange: (v: string) => void;
}

export default function TextInputCard({ value, onChange }: Props) {
  return (
    <div className="card">
      <h3>Patient Statement / Note</h3>
      <textarea
        rows={5}
        placeholder="Enter patient statement..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}
