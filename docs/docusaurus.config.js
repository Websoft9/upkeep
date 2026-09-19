// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'UpKeep Docs',
  tagline: 'AI-driven predictive maintenance for industrial robots',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://websoft9.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served.
  // For GitHub pages deployment it is often '/<projectName>/'.
  baseUrl: '/upkeep/',

  // GitHub pages deployment config.
  organizationName: 'Websoft9',
  projectName: 'upkeep',

  onBrokenLinks: 'throw',

  // Product documentation is authored in English by default.
  // Add locales here (for example 'zh-Hans') when translations are ready.
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Remove this to remove the "edit this page" links.
          editUrl: 'https://github.com/Websoft9/upkeep/tree/main/docs/',
        },
        // UpKeep publishes product documentation only; there is no blog.
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      colorMode: {
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: 'UpKeep',
        logo: {
          alt: 'UpKeep Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'docsSidebar',
            position: 'left',
            label: 'Documentation',
          },
          {
            href: 'https://github.com/Websoft9/upkeep',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Introduction',
                to: '/docs/intro',
              },
              {
                label: 'Quickstart',
                to: '/docs/getting-started/quickstart',
              },
              {
                label: 'API Reference',
                to: '/docs/api/overview',
              },
            ],
          },
          {
            title: 'Product',
            items: [
              {
                label: 'Business Brief',
                to: '/docs/product/business-brief',
              },
              {
                label: 'MVP PRD',
                to: '/docs/product/mvp-prd',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/Websoft9/upkeep',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Websoft9. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
