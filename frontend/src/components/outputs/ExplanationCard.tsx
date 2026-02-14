interface Props {
  text?: string;
}

export default function ExplanationCard({ text }: Props) {
  if (!text) return null;

  return (
    <div className="card">
      <h3>Explanation</h3>
      <p>{text}</p>
    </div>
  );
}
