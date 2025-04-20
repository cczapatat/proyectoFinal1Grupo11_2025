package com.smartstock.myapplication.orders


import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView.ViewHolder
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.UiController
import androidx.test.espresso.ViewAction
import androidx.test.espresso.action.ViewActions.*
import androidx.test.espresso.assertion.ViewAssertions.*
import androidx.test.espresso.contrib.RecyclerViewActions.actionOnItemAtPosition
import androidx.test.espresso.matcher.RootMatchers
import androidx.test.espresso.matcher.ViewMatchers.*
import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.LargeTest
import com.smartstock.myapplication.R
import com.smartstock.myapplication.SplashActivity
import com.smartstock.myapplication.Utils
import org.hamcrest.Description
import org.hamcrest.Matcher
import org.hamcrest.Matchers.allOf
import org.hamcrest.Matchers.`is`
import org.hamcrest.TypeSafeMatcher
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@LargeTest
@RunWith(AndroidJUnit4::class)
class CreateOrderTest {

    @Rule
    @JvmField
    var mActivityScenarioRule = ActivityScenarioRule(SplashActivity::class.java)

    fun waitFor(millis: Long): ViewAction {
        return object : ViewAction {
            override fun getConstraints(): Matcher<View> = isRoot()

            override fun getDescription(): String = "Wait for $millis milliseconds."

            override fun perform(uiController: UiController, view: View?) {
                uiController.loopMainThreadForAtLeast(millis)
            }
        }
    }
    @Test
    fun createOrderTest() {
        onView(isRoot()).perform(waitFor(4000))
        val textInputEditText = onView(withId(R.id.email))
            .perform(replaceText("cliente1@sta.com"), closeSoftKeyboard())

        val textInputEditText2 = onView(withId(R.id.password))
            .perform(replaceText("1234567"), closeSoftKeyboard())

        val materialButton = onView(withId(R.id.buttonLogin))
            .perform(click())

        onView(isRoot()).perform(waitFor(5000))
        val bottomNavigationItemView = onView(
            withId(R.id.nav_menu)
        )
        bottomNavigationItemView.perform(click())
        onView(isRoot()).perform(waitFor(1000))

        val materialTextView = onView(
            allOf(
                withId(android.R.id.title), withText(Utils.getLocalizedText("create_order")),
                childAtPosition(
                    childAtPosition(
                        withId(android.R.id.content),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        materialTextView.perform(click())

        onView(withId(R.id.textField4_6))
            .perform(click())

        onView(isRoot()).perform(waitFor(100))

        // Click the first item in the dropdown
        onView(withText(Utils.getLocalizedText("tipo_pago_ondelivery"))) // Replace with actual string shown in the list
            .inRoot(RootMatchers.isPlatformPopup()) // This tells Espresso to look in the dropdown popup
            .perform(click())


        onView(isRoot()).perform(waitFor(1000))
        onView(withId(R.id.buttonAddProduct))
            .check(matches(isDisplayed()))
            .check(matches(isEnabled()))
            .perform(click())

        onView(isRoot()).perform(waitFor(1000))
        //////////////////////**///

        val recyclerView = onView(
            allOf(
                withId(R.id.productRecyclerView),
                childAtPosition(
                    withId(R.id.add_producto_section_2),
                    0
                )
            )
        )
        recyclerView.perform(actionOnItemAtPosition<ViewHolder>(0, click()))

        val textInputEditText4 = onView(
            allOf(
                withId(R.id.quantityInput),
                childAtPosition(
                    childAtPosition(
                        withId(R.id.textField6_1),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        textInputEditText4.perform(replaceText("20"), closeSoftKeyboard())

        val textInputEditText5 = onView(
            allOf(
                withId(R.id.quantityInput), withText("20"),
                childAtPosition(
                    childAtPosition(
                        withId(R.id.textField6_1),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        textInputEditText5.perform(pressImeActionButton())

        val materialButton3 = onView(
            allOf(
                withId(android.R.id.button1), withText(Utils.getLocalizedText("add")),
                childAtPosition(
                    childAtPosition(
                        withClassName(`is`("android.widget.ScrollView")),
                        0
                    ),
                    3
                )
            )
        )
        materialButton3.perform(scrollTo(), click())


        onView(isRoot()).perform(waitFor(1000))
        onView(withId(R.id.buttonAcceptCreate))
            .check(matches(isDisplayed()))
            .check(matches(isEnabled()))
            .perform(click())

        onView(isRoot()).perform(waitFor(3000))

        val textViewPPal = onView(withId(R.id.client_list))
        textViewPPal.check(matches(withText(Utils.getLocalizedText("lista_de_clientes"))))

    }

    private fun childAtPosition(
        parentMatcher: Matcher<View>, position: Int
    ): Matcher<View> {

        return object : TypeSafeMatcher<View>() {
            override fun describeTo(description: Description) {
                description.appendText("Child at position $position in parent ")
                parentMatcher.describeTo(description)
            }

            public override fun matchesSafely(view: View): Boolean {
                val parent = view.parent
                return parent is ViewGroup && parentMatcher.matches(parent)
                        && view == parent.getChildAt(position)
            }
        }
    }
}
