import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Telemetry in, insights out',
    description: (
      <>
        Push time-series data from external providers and get normalized,
        vendor-neutral robot context in return.
      </>
    ),
  },
  {
    title: 'Explainable recommendations',
    description: (
      <>
        Every recommendation carries the metric, observed value, threshold, and
        source telemetry id so it can be traced and audited.
      </>
    ),
  },
  {
    title: 'Built for fixed robot cells',
    description: (
      <>
        A focused MVP for fixed industrial robots that grows toward more robot
        types, vendors, and integrations.
      </>
    ),
  },
];

function Feature({title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
