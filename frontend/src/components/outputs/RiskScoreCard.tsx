interface Props {
  score?: number;
}

export default function RiskScoreCard({ score }: Props) {
  if (score === undefined) return null;

  return (
    <div className="card">
      <h3>Risk Score</h3>
      <p style={{ fontSize: "24px", fontWeight: "bold" }}>{score}</p>
    </div>
  );
}
