import Nav from '@/components/Nav'
import Hero from '@/components/Hero'
import ProblemSection from '@/components/ProblemSection'
import ApproachSection from '@/components/ApproachSection'
import ArchitectureSection from '@/components/ArchitectureSection'
import ScopeSection from '@/components/ScopeSection'
import DashboardSection from '@/components/DashboardSection'
import FAQSection from '@/components/FAQSection'
import Footer from '@/components/Footer'

export default function Page() {
  return (
    <>
      <Nav />
      <main>
        <Hero />
        <ProblemSection />
        <ApproachSection />
        <ArchitectureSection />
        <ScopeSection />
        <DashboardSection />
        <FAQSection />
      </main>
      <Footer />
    </>
  )
}
